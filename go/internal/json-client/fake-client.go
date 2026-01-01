//go:build fake

package jsonclient

import (
	"context"
	"crypto/tls"
	"fmt"
	"net/http"
	"net/url"

	azcore "github.com/microsoft/kiota-abstractions-go"
	graph "github.com/microsoftgraph/msgraph-sdk-go"

	"github.com/pzsp-teams/lib/config"
	"github.com/pzsp-teams/lib"
	jsonModel "github.com/pzsp-teams/lib-python/internal/json-model"
)

// --- 1. Fake Auth Provider ---
type FakeAuthProvider struct{}

func (f *FakeAuthProvider) AuthenticateRequest(ctx context.Context, request *azcore.RequestInformation, additionalAuthenticationContext map[string]interface{}) error {
	if request.Headers == nil {
		request.Headers = azcore.NewRequestHeaders()
	}
	request.Headers.Add("Authorization", "Bearer fake-jwt-token")

	return nil
}

// --- 2. Replace MS API with Python Mock Server ---
type HijackTransport struct {
	MockServerURL string
	Transport     http.RoundTripper
}

func (t *HijackTransport) RoundTrip(req *http.Request) (*http.Response, error) {
	parsed, err := url.Parse(t.MockServerURL)
	if err != nil {
		return nil, err
	}

	req.URL.Scheme = parsed.Scheme
	req.URL.Host = parsed.Host

	return t.Transport.RoundTrip(req)
}

// --- 3. Fake JSON Client Factory ---
func NewJSONClient(req jsonModel.Request) (*TeamsJSONClient, error) {
	// Parse parameters
	mockServerURL, ok := req.Params["mockServerUrl"].(string)
	if !ok || mockServerURL == "" {
		return nil, fmt.Errorf("invalid mockServerUrl parameter")
	}

	senderConfig := config.SenderConfig{
		MaxRetries:     3,
		NextRetryDelay: 2,
		Timeout:        5,
	}

	cacheConfig := config.CacheConfig{
		Mode: config.CacheDisabled,
		Provider: config.CacheProviderJSONFile,
		Path: nil,
	}

	hijackedHttpClient := &http.Client{
		Transport: &HijackTransport{
			MockServerURL: mockServerURL,
			Transport: &http.Transport{
				TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
			},
		},
	}
	authProvider := &FakeAuthProvider{}

	adapter, err := graph.NewGraphRequestAdapterWithParseNodeFactoryAndSerializationWriterFactoryAndHttpClient(
		authProvider,
		nil, // default ParseNodeFactory
		nil, // default SerializationWriterFactory
		hijackedHttpClient,
	)
	if err != nil {
		return nil, err
	}

	graphClient := graph.NewGraphServiceClient(adapter)

	client, err := lib.NewClientFromGraphClient(graphClient, &senderConfig, &cacheConfig)
	if err != nil {
		return nil, err
	}

	return &TeamsJSONClient{client}, nil
}
