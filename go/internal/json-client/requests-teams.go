package jsonclient

import (
	"context"

	"github.com/pzsp-teams/lib-python/internal/json-client/decoders"
)

type getTeamParams struct {
	TeamRef string `json:"teamRef"`
}

func (c *TeamsJSONClient) GetTeam(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params getTeamParams) (interface{}, error) {
		return c.client.Teams.Get(context.TODO(), params.TeamRef)
	})
}

func (c *TeamsJSONClient) ListMyJoined() (interface{}, error) {
	return c.client.Teams.ListMyJoined(context.TODO())
}

type updateTeamParams struct {
	TeamRef   string                `json:"teamRef"`
	TeamPatch decoders.TeamPatchDTO `json:"team"`
}

func (c *TeamsJSONClient) UpdateTeam(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params updateTeamParams) (interface{}, error) {
		msTeam := decoders.GetMSTeam(&params.TeamPatch)
		return c.client.Teams.Update(context.TODO(), params.TeamRef, msTeam)
	})
}

type createViaGroupParams struct {
	DisplayName  string `json:"displayName"`
	MailNickname string `json:"mailNickname"`
	Visibility   string `json:"visibility"`
}

func (c *TeamsJSONClient) CreateTeamViaGroup(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params createViaGroupParams) (interface{}, error) {
		return c.client.Teams.CreateViaGroup(context.TODO(), params.DisplayName, params.MailNickname, params.Visibility)
	})
}

type createFromTemplateParams struct {
	DisplayName string   `json:"displayName"`
	Description string   `json:"description"`
	Owners      []string `json:"owners"`
}

func (c *TeamsJSONClient) CreateTeamFromTemplate(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params createFromTemplateParams) (interface{}, error) {
		return c.client.Teams.CreateFromTemplate(context.TODO(), params.DisplayName, params.Description, params.Owners)
	})
}

type archiveTeamParams struct {
	TeamRef                string `json:"teamRef"`
	SpoReadOnlyFromMembers *bool  `json:"spoReadOnlyFromMembers,omitempty"`
}

func (c *TeamsJSONClient) ArchiveTeam(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params archiveTeamParams) (interface{}, error) {
		err := c.client.Teams.Archive(context.TODO(), params.TeamRef, params.SpoReadOnlyFromMembers)
		return "archived", err
	})
}

type unarchiveTeamParams struct {
	TeamRef string `json:"teamRef"`
}

func (c *TeamsJSONClient) UnarchiveTeam(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params unarchiveTeamParams) (interface{}, error) {
		err := c.client.Teams.Unarchive(context.TODO(), params.TeamRef)
		return "unarchived", err
	})
}

type deleteTeamParams struct {
	TeamRef string `json:"teamRef"`
}

func (c *TeamsJSONClient) DeleteTeam(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params deleteTeamParams) (interface{}, error) {
		err := c.client.Teams.Delete(context.TODO(), params.TeamRef)
		return "deleted", err
	})
}

type restoreTeamParams struct {
	DeletedGroupID string `json:"deletedGroupId"`
}

func (c *TeamsJSONClient) RestoreDeletedTeam(p map[string]interface{}) (interface{}, error) {
	return execute(p, func(params restoreTeamParams) (interface{}, error) {
		return c.client.Teams.RestoreDeleted(context.TODO(), params.DeletedGroupID)
	})
}