package jsonmodel

import (
	"fmt"

	"github.com/pzsp-teams/lib"
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
}

type SenderConfigMap struct {
	MaxRetries     int `json:"maxRetries"`
	NextRetryDelay int `json:"nextRetryDelay"`
	Timeout        int `json:"timeout"`
}

func (scm SenderConfigMap) ToSenderConfig() (lib.SenderConfig, error) {
    if scm.MaxRetries < 0 {
        return lib.SenderConfig{}, fmt.Errorf("maxRetries cannot be negative")
    }
    if scm.NextRetryDelay < 0 {
        return lib.SenderConfig{}, fmt.Errorf("nextRetryDelay cannot be negative")
    }
    if scm.Timeout <= 0 {
        return lib.SenderConfig{}, fmt.Errorf("timeout must be > 0")
    }

    return lib.SenderConfig{
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

func (acm AuthConfigMap) ToAuthConfig() (lib.AuthConfig, error) {
    if acm.ClientID == "" {
        return lib.AuthConfig{}, fmt.Errorf("clientId is required")
    }
    if acm.Tenant == "" {
        return lib.AuthConfig{}, fmt.Errorf("tenant is required")
    }
    if acm.Email == "" {
        return lib.AuthConfig{}, fmt.Errorf("email is required")
    }
    if len(acm.Scopes) == 0 {
        return lib.AuthConfig{}, fmt.Errorf("scopes cannot be empty")
    }
    if acm.AuthMethod == "" {
        return lib.AuthConfig{}, fmt.Errorf("authMethod is required")
    }

    authMethod, err := validateAuthMethod(acm.AuthMethod)
    if err != nil {
        return lib.AuthConfig{}, err
    }

    return lib.AuthConfig{
        ClientID:   acm.ClientID,
        Tenant:     acm.Tenant,
        Email:      acm.Email,
        Scopes:     acm.Scopes,
        AuthMethod: authMethod,
    }, nil
}

func validateAuthMethod(method string) (string, error) {
	if method == "DEVICE_CODE" || method == "INTERACTIVE" {
		return method, nil
	}
	return "", fmt.Errorf("invalid auth method: %s", method)
}

