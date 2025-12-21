package jsonclient

import (
	"context"

	"github.com/pzsp-teams/lib-python/internal/decoders"
)

type getTeamParams struct {
	TeamRef string `json:"teamRef"`
}

func (jsonclient *TeamsJSONClient) Get(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[getTeamParams](p)
	if err != nil {
		return nil, err
	}
	team, err := jsonclient.client.Teams.Get(context.TODO(), params.TeamRef)
	if err != nil {
		return nil, err
	} else {
		return team, nil
	}
}

func (jsonclient *TeamsJSONClient) ListMyJoined() (interface{}, error) {
	teams, err := jsonclient.client.Teams.ListMyJoined(context.TODO())
	if err != nil {
		return nil, err
	} else {
		return teams, nil
	}
}

type updateTeamParams struct {
	TeamRef   string                `json:"teamRef"`
	TeamPatch decoders.TeamPatchDTO `json:"team"`
}

func (jsonclient *TeamsJSONClient) Update(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[updateTeamParams](p)
	msTeam := decoders.GetMSTeam(&params.TeamPatch)
	if err != nil {
		return nil, err
	}
	updatedTeam, err := jsonclient.client.Teams.Update(context.TODO(), params.TeamRef, msTeam)
	if err != nil {
		return nil, err
	} else {
		return updatedTeam, nil
	}
}
