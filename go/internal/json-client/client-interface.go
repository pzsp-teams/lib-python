package jsonclient

import (
	"context"

	lib "github.com/pzsp-teams/lib"
	models "github.com/pzsp-teams/lib/models"
)

type TeamsJSONClient interface {
	Teams() teamsService
	Channels() channelsService
}

type teamsService interface {
	ListMyJoined(ctx context.Context) ([]*models.Team, error)
}

type channelsService interface {
	ListChannels(ctx context.Context, team string) ([]*models.Channel, error)
	ListMessages(ctx context.Context, team, channel string, opts *models.ListMessagesOptions) ([]*models.Message, error)
}

type clientAdapter struct {
	client *lib.Client
}

func (c *clientAdapter) Teams() teamsService {
	return c.client.Teams
}

func (c *clientAdapter) Channels() channelsService {
	return c.client.Channels
}
