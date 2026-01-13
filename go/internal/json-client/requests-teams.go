package jsonclient

import (
	"context"

	"github.com/pzsp-teams/lib-python/internal/json-client/decoders"
)

type getTeamParams struct {
	TeamRef string `json:"teamRef"`
}

func (c *TeamsJSONClient) GetTeam(p map[string]any) (any, error) {
	return execute(p, func(params getTeamParams) (any, error) {
		return c.client.Teams.Get(context.TODO(), params.TeamRef)
	})
}

func (c *TeamsJSONClient) ListMyJoined() (any, error) {
	return c.client.Teams.ListMyJoined(context.TODO())
}

type updateTeamParams struct {
	TeamRef    string                 `json:"teamRef"`
	TeamUpdate decoders.UpdateTeamDTO `json:"team"`
}

func (c *TeamsJSONClient) UpdateTeam(p map[string]any) (any, error) {
	return execute(p, func(params updateTeamParams) (any, error) {
		updateTeam := decoders.GetUpdateTeam(&params.TeamUpdate)
		return c.client.Teams.UpdateTeam(context.TODO(), params.TeamRef, &updateTeam)
	})
}

type createViaGroupParams struct {
	DisplayName  string `json:"displayName"`
	MailNickname string `json:"mailNickname"`
	Visibility   string `json:"visibility"`
}

func (c *TeamsJSONClient) CreateTeamViaGroup(p map[string]any) (any, error) {
	return execute(p, func(params createViaGroupParams) (any, error) {
		return c.client.Teams.CreateViaGroup(context.TODO(), params.DisplayName, params.MailNickname, params.Visibility)
	})
}

type createFromTemplateParams struct {
	DisplayName string   `json:"displayName"`
	Description string   `json:"description"`
	Owners      []string `json:"owners"`
	Members     []string `json:"members"`
	Visibility  string   `json:"visibility"`
	IncludeMe   bool     `json:"includeMe"`
}

func (c *TeamsJSONClient) CreateTeamFromTemplate(p map[string]any) (any, error) {
	return execute(p, func(params createFromTemplateParams) (any, error) {
		return c.client.Teams.CreateFromTemplate(context.TODO(), params.DisplayName, params.Description, params.Owners, params.Members, params.Visibility, params.IncludeMe)
	})
}

type archiveTeamParams struct {
	TeamRef                string `json:"teamRef"`
	SpoReadOnlyFromMembers *bool  `json:"spoReadOnlyFromMembers,omitempty"`
}

func (c *TeamsJSONClient) ArchiveTeam(p map[string]any) (any, error) {
	return execute(p, func(params archiveTeamParams) (any, error) {
		err := c.client.Teams.Archive(context.TODO(), params.TeamRef, params.SpoReadOnlyFromMembers)
		return "archived", err
	})
}

type unarchiveTeamParams struct {
	TeamRef string `json:"teamRef"`
}

func (c *TeamsJSONClient) UnarchiveTeam(p map[string]any) (any, error) {
	return execute(p, func(params unarchiveTeamParams) (any, error) {
		err := c.client.Teams.Unarchive(context.TODO(), params.TeamRef)
		return "unarchived", err
	})
}

type deleteTeamParams struct {
	TeamRef string `json:"teamRef"`
}

func (c *TeamsJSONClient) DeleteTeam(p map[string]any) (any, error) {
	return execute(p, func(params deleteTeamParams) (any, error) {
		err := c.client.Teams.Delete(context.TODO(), params.TeamRef)
		return "deleted", err
	})
}

type restoreTeamParams struct {
	DeletedGroupID string `json:"deletedGroupId"`
}

func (c *TeamsJSONClient) RestoreDeletedTeam(p map[string]any) (any, error) {
	return execute(p, func(params restoreTeamParams) (any, error) {
		return c.client.Teams.RestoreDeleted(context.TODO(), params.DeletedGroupID)
	})
}
