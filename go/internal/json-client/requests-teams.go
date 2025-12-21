package jsonclient

import (
	"context"

	"github.com/pzsp-teams/lib-python/internal/json-client/decoders"
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
	}
	return team, nil
}

func (jsonclient *TeamsJSONClient) ListMyJoined() (interface{}, error) {
	teams, err := jsonclient.client.Teams.ListMyJoined(context.TODO())
	if err != nil {
		return nil, err
	}
	return teams, nil
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
	}
	return updatedTeam, nil
}

type createViaGroupParams struct {
	DisplayName  string `json:"displayName"`
	MailNickname string `json:"mailNickname"`
	Visibility   string `json:"visibility"`
}

func (jsonclient *TeamsJSONClient) CreateViaGroup(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[createViaGroupParams](p)
	if err != nil {
		return nil, err
	}
	createdTeam, err := jsonclient.client.Teams.CreateViaGroup(context.TODO(), params.DisplayName, params.MailNickname, params.Visibility)
	if err != nil {
		return nil, err
	}
	return createdTeam, nil
}

type createFromTemplateParams struct {
	DisplayName string   `json:"displayName"`
	Description string   `json:"description"`
	Owners      []string `json:"owners"`
}

func (jsonclient *TeamsJSONClient) CreateFromTemplate(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[createFromTemplateParams](p)
	if err != nil {
		return nil, err
	}
	createdTeam, err := jsonclient.client.Teams.CreateFromTemplate(context.TODO(), params.DisplayName, params.Description, params.Owners)
	if err != nil {
		return nil, err
	}
	return createdTeam, nil
}

type archiveTeamParams struct {
	TeamRef string `json:"teamRef"`
	SpoReadOnlyFromMembers *bool  `json:"spoReadOnlyFromMembers,omitempty"`
}

func (jsonclient *TeamsJSONClient) Archive(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[archiveTeamParams](p)
	if err != nil {
		return nil, err
	}
	err = jsonclient.client.Teams.Archive(context.TODO(), params.TeamRef, params.SpoReadOnlyFromMembers)
	if err != nil {
		return nil, err
	}
	return "archived", nil
}

type unarchiveTeamParams struct {
	TeamRef string `json:"teamRef"`
}

func (jsonclient *TeamsJSONClient) Unarchive(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[unarchiveTeamParams](p)
	if err != nil {
		return nil, err
	}
	err = jsonclient.client.Teams.Unarchive(context.TODO(), params.TeamRef)
	if err != nil {
		return nil, err
	}
	return "unarchived", nil
}

type deleteTeamParams struct {
	TeamRef string `json:"teamRef"`
}

func (jsonclient *TeamsJSONClient) Delete(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[deleteTeamParams](p)
	if err != nil {
		return nil, err
	}
	err = jsonclient.client.Teams.Delete(context.TODO(), params.TeamRef)
	if err != nil {
		return nil, err
	}
	return "deleted", nil
}

type restoreTeamParams struct {
	DeletedGroupID string `json:"deletedGroupId"`
}

func (jsonclient *TeamsJSONClient) RestoreDeleted(p map[string]interface{}) (interface{}, error) {
	params, err := decoders.DecodeParams[restoreTeamParams](p)
	if err != nil {
		return nil, err
	}
	restoredTeam, err := jsonclient.client.Teams.RestoreDeleted(context.TODO(), params.DeletedGroupID)
	if err != nil {
		return nil, err
	}
	return restoredTeam, nil
}
