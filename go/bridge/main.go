package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"os"

	jsonClient "github.com/pzsp-teams/lib-python/internal/json-client"
	jsonModel "github.com/pzsp-teams/lib-python/internal/json-model"
)

var client *jsonClient.TeamsJSONClient
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

			c, err := jsonClient.NewRealJSONClient(req)
			if detectFail(writer, err) {
				continue
			}

			client = c
			initialized = true
			respondResult(writer, "initialized")
			continue
		}

		if req.Type == "initFake" {
			if initialized {
				respondError(writer, fmt.Errorf("client already initialized"))
				continue
			}

			c, err := jsonClient.NewFakeJSONClient(req)
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

			switch req.Method {
			case "listChannels":
				channels, err := client.ListChannels(req.Params)
				if err != nil {
					respondError(writer, err)
				} else {
					respondResult(writer, channels)
				}
			default:
				respondError(writer, fmt.Errorf("unknown method"))
			}
			continue
		}
		respondError(writer, fmt.Errorf("unknown request type"))
	}
}
