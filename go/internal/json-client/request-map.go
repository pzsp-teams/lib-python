package jsonclient

type HandlerFunc func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error)

var Handlers = map[string]HandlerFunc{

	"listChannels": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.ListChannels(p)
	},

	"getTeam": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.GetTeam(p)
	},

	"updateTeam": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.UpdateTeam(p)
	},

	"listMyJoined": func(c *TeamsJSONClient, _ map[string]interface{}) (interface{}, error) {
		return c.ListMyJoined()
	},

	"createTeamViaGroup": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.CreateTeamViaGroup(p)
	},

	"createTeamFromTemplate": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.CreateTeamFromTemplate(p)
	},

	"archiveTeam": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.ArchiveTeam(p)
	},

	"unarchiveTeam": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.UnarchiveTeam(p)
	},

	"deleteTeam": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.DeleteTeam(p)
	},

	"restoreDeletedTeam": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.RestoreDeletedTeam(p)
	},
}
