package main

import (
	"bufio"
	"encoding/json"
)

type response struct {
	Result interface{} `json:"result,omitempty"`
	Error  string      `json:"error,omitempty"`
}

func detectFail(writer *bufio.Writer, err error) bool {
	if err != nil {
		respondError(writer, err)
		return true
	}
	return false
}


func respondError(writer *bufio.Writer, err error) {
	response := response{
		Error: err.Error(),
	}
	respBytes, _ := json.Marshal(response)
	writer.Write(respBytes)
	writer.WriteString("\n")
	writer.Flush()
}

func respondResult(writer *bufio.Writer, result interface{}) {
	response := response{
		Result: result,
	}
	respBytes, _ := json.Marshal(response)
	writer.Write(respBytes)
	writer.WriteString("\n")
	writer.Flush()
}