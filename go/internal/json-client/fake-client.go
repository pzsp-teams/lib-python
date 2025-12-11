//go:build fake

package jsonclient

import (
	"context"
	"fmt"
	"crypto/tls"
	"net/http"
	"strings"

	azcore "github.com/microsoft/kiota-abstractions-go"
	graph "github.com/microsoftgraph/msgraph-sdk-go"

	lib "github.com/pzsp-teams/lib"
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
	req.URL.Scheme = "http"

	targetHost := strings.TrimPrefix(t.MockServerURL, "http://")
	targetHost = strings.TrimPrefix(targetHost, "https://")
	req.URL.Host = targetHost

	return t.Transport.RoundTrip(req)
}

// --- 3. Fake JSON Client Factory ---
func NewFakeJSONClient(req jsonModel.Request) (*TeamsJSONClient, error) {
	// Parse parameters
	mockServerURL, ok := req.Params["mockServerUrl"].(string)
	if !ok || mockServerURL == "" {
		return nil,  fmt.Errorf("invalid mockServerUrl parameter")
	}

	// A. Konfiguracja SenderConfig (tak jak w wersji Real)
	senderConfig := lib.SenderConfig{
		MaxRetries:     3,
		NextRetryDelay: 2,
		Timeout:        5,
	}

	cacheEnabled := false
	var cachePath *string = nil

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

	client, err := lib.NewClientFromGraphClient(graphClient, &senderConfig, cacheEnabled, cachePath)
	if err != nil {
		return nil, err
	}

	return &TeamsJSONClient{client}, nil
}
