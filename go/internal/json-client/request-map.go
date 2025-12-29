package jsonclient

type HandlerFunc func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error)

var Handlers = map[string]HandlerFunc{

	// TEAMS
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

	// CHANNELS
	"listChannels": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.ListChannels(p)
	},

	"getChannel": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.GetChannel(p)
	},

	"createStandardChannel": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.CreateStandardChannel(p)
	},

	"createPrivateChannel": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.CreatePrivateChannel(p)
	},

	"deleteChannel": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.DeleteChannel(p)
	},

	"listChannelMembers": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.ListChannelMembers(p)
	},

	"addMemberToChannel": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.AddMemberToChannel(p)
	},

	"removeMemberFromChannel": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.RemoveMemberFromChannel(p)
	},

	"updateMemberRoleInChannel": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.UpdateMemberInChannel(p)
	},

	"sendMessageToChannel": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.SendMessageToChannel(p)
	},

	"listMessagesInChannel": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.ListMessagesInChannel(p)
	},

	"getMessageInChannel": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.GetMessageInChannel(p)
	},

	"listMessageRepliesInChannel": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.ListMessageRepliesInChannel(p)
	},

	"getMessageReplyInChannel": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.GetMessageReplyInChannel(p)
	},

	// CHATS
	"createOneOnOneChat": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.CreateOneToOneChat(p)
	},

	"createGroupChat": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.CreateGroupChat(p)
	},

	"sendMessageInChat": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.SendMessageInChat(p)
	},

	"listMyChats": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.ListMyChats(p)
	},

	"listMembersInChat": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.ListMembersInChat(p)
	},

	"addMemberToChat": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.AddMemberToChat(p)
	},
}
