package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"os"

	jsonClientLib "github.com/pzsp-teams/lib-python/internal/json-client"
	jsonModel "github.com/pzsp-teams/lib-python/internal/json-model"
)

var client *jsonClientLib.TeamsJSONClient
var initialized bool

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Buffer(make([]byte, 0, 1024), 1024*1024)
	writer := bufio.NewWriter(os.Stdout)

	for scanner.Scan() {
		line := scanner.Text()

		var req jsonModel.Request
		err := json.Unmarshal([]byte(line), &req)
		if err != nil {
			respondError(writer, fmt.Errorf("invalid json: %w", err))
			continue
		}

		if req.Type == "init" {
			if initialized {
				respondError(writer, fmt.Errorf("client already initialized"))
				continue
			}

			c, err := jsonClientLib.NewJSONClient(req)
			if detectFail(writer, err) {
				continue
			}

			client = c
			initialized = true
			respondResult(writer, "initialized")
			continue
		}

		if req.Type == "request" {
			if client == nil {
				respondError(writer, fmt.Errorf("client not initialized"))
				continue
			}

			handler, exists := jsonClientLib.Handlers[req.Method]
			if !exists {
				respondError(writer, fmt.Errorf("unknown method"))
				continue
			}

			result, err := handler(client, req.Params)
			if err != nil {
				respondError(writer, err)
			}
			respondResult(writer, result)
			continue
		}
	}
}
