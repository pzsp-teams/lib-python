package jsonmodel

import (
	"fmt"

	"github.com/pzsp-teams/lib/config"
)

type Request struct {
	Type   string                 `json:"type"`
	Method string                 `json:"method,omitempty"`
	Config Config                 `json:"config,omitempty"`
	Params map[string]interface{} `json:"params,omitempty"`
}

type Config struct {
	SenderConfigMap SenderConfigMap `json:"senderConfig"`
	AuthConfigMap   AuthConfigMap   `json:"authConfig"`
	CacheMode       string          `json:"cacheMode,omitempty"`
	CachePath       string          `json:"cachePath,omitempty"`
}

type SenderConfigMap struct {
	MaxRetries     int `json:"maxRetries"`
	NextRetryDelay int `json:"nextRetryDelay"`
	Timeout        int `json:"timeout"`
}

func (scm SenderConfigMap) ToSenderConfig() (*config.SenderConfig, error) {
	if scm.MaxRetries < 0 {
		return nil, fmt.Errorf("maxRetries cannot be negative")
	}
	if scm.NextRetryDelay < 0 {
		return nil, fmt.Errorf("nextRetryDelay cannot be negative")
	}
	if scm.Timeout <= 0 {
		return nil, fmt.Errorf("timeout must be > 0")
	}

	return &config.SenderConfig{
		MaxRetries:     scm.MaxRetries,
		NextRetryDelay: scm.NextRetryDelay,
		Timeout:        scm.Timeout,
	}, nil
}

type AuthConfigMap struct {
	ClientID   string   `json:"clientId"`
	Tenant     string   `json:"tenant"`
	Email      string   `json:"email"`
	Scopes     []string `json:"scopes"`
	AuthMethod string   `json:"authMethod"`
}

func (acm AuthConfigMap) ToAuthConfig() (*config.AuthConfig, error) {
	if acm.ClientID == "" {
		return nil, fmt.Errorf("clientId is required")
	}
	if acm.Tenant == "" {
		return nil, fmt.Errorf("tenant is required")
	}
	if acm.Email == "" {
		return nil, fmt.Errorf("email is required")
	}
	if len(acm.Scopes) == 0 {
		return nil, fmt.Errorf("scopes cannot be empty")
	}
	if acm.AuthMethod == "" {
		return nil, fmt.Errorf("authMethod is required")
	}

	authMethod, err := validateAuthMethod(acm.AuthMethod)
	if err != nil {
		return nil, err
	}

	return &config.AuthConfig{
		ClientID:   acm.ClientID,
		Tenant:     acm.Tenant,
		Email:      acm.Email,
		Scopes:     acm.Scopes,
		AuthMethod: config.Method(authMethod),
	}, nil
}

func ParseCachePath(value interface{}) (*string, error) {
	path, ok := value.(string)
	if !ok || path == "" {
		return nil, fmt.Errorf("cachePath must be a non-empty string")
	}
	return &path, nil
}

func ParseCacheMode(value interface{}) (config.CacheMode, error) {
	switch value {
	case "DISABLED":
		return config.CacheDisabled, nil
	case "SYNC":
		return config.CacheSync, nil
	case "ASYNC":
		return config.CacheAsync, nil
	default:
		return config.CacheDisabled, fmt.Errorf("invalid cacheMode: %s", value)
	}
}

func validateAuthMethod(method string) (string, error) {
	if method == "DEVICE_CODE" || method == "INTERACTIVE" {
		return method, nil
	}
	return "", fmt.Errorf("invalid auth method: %s", method)
}
