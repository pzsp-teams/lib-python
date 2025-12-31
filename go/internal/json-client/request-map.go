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

	"sendMessageToChannel": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.SendMessageToChannel(p)
	},

	"sendReplyToChannel": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.SendReplyToChannel(p)
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

	"getMentionsInChannel": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.GetMentionsInChannel(p)
	},

	// CHATS
	"createOneOnOneChat": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.CreateOneToOneChat(p)
	},

	"createGroupChat": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.CreateGroupChat(p)
	},

	"addMemberGroupToChat": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.AddMemberGroupToChat(p)
	},

	"removeMemberFromGroupChat": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.RemoveMemberFromGroupChat(p)
	},

	"listMembersInGroupChat": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.ListGroupChatMembers(p)
	},

	"updateGroupChatTopic": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.UpdateGroupChatTopic(p)
	},

	"listMessagesInChat": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.ListMessagesInChat(p)
	},

	"sendMessageInChat": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.SendMessageInChat(p)
	},

	"deleteMessageInChat": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.DeleteMessageInChat(p)
	},

	"getMessageInChat": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.GetMessageInChat(p)
	},

	"listMyChats": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.ListMyChats(p)
	},

	"listMyChatMessages": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.ListMyChatMessages(p)
	},

	"listPinnedMessagesInChat": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.ListPinnedMessagesInChat(p)
	},

	"pinMessageInChat": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.PinMessageInChat(p)
	},

	"unpinMessageInChat": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.UnpinMessageInChat(p)
	},

	"getMentionsInChat": func(c *TeamsJSONClient, p map[string]interface{}) (interface{}, error) {
		return c.GetMentionsInChat(p)
	},
}
