package jsonclient

import (
	"context"
)

type HandlerFunc func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error)

var Handlers = map[string]HandlerFunc{

	// TEAMS
	"getTeam": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.GetTeam(ctx, p)
	},

	"updateTeam": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.UpdateTeam(ctx, p)
	},

	"listMyJoined": func(c *TeamsJSONClient, ctx context.Context, _ map[string]any) (any, error) {
		return c.ListMyJoined(ctx)
	},

	"createTeamViaGroup": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.CreateTeamViaGroup(ctx, p)
	},

	"createTeamFromTemplate": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.CreateTeamFromTemplate(ctx, p)
	},

	"archiveTeam": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.ArchiveTeam(ctx, p)
	},

	"unarchiveTeam": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.UnarchiveTeam(ctx, p)
	},

	"deleteTeam": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.DeleteTeam(ctx, p)
	},

	"restoreDeletedTeam": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.RestoreDeletedTeam(ctx, p)
	},

	// CHANNELS
	"listChannels": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.ListChannels(ctx, p)
	},

	"getChannel": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.GetChannel(ctx, p)
	},

	"createStandardChannel": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.CreateStandardChannel(ctx, p)
	},

	"createPrivateChannel": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.CreatePrivateChannel(ctx, p)
	},

	"deleteChannel": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.DeleteChannel(ctx, p)
	},

	"sendMessageToChannel": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.SendMessageToChannel(ctx, p)
	},

	"sendReplyToChannel": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.SendReplyToChannel(ctx, p)
	},

	"listMessagesInChannel": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.ListMessagesInChannel(ctx, p)
	},

	"getMessageInChannel": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.GetMessageInChannel(ctx, p)
	},

	"listMessageRepliesInChannel": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.ListMessageRepliesInChannel(ctx, p)
	},

	"getMessageReplyInChannel": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.GetMessageReplyInChannel(ctx, p)
	},

	"listChannelMembers": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.ListChannelMembers(ctx, p)
	},

	"addMemberToChannel": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.AddMemberToChannel(ctx, p)
	},

	"removeMemberFromChannel": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.RemoveMemberFromChannel(ctx, p)
	},

	"updateMemberRoleInChannel": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.UpdateMemberInChannel(ctx, p)
	},

	"getMentionsInChannel": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.GetMentionsInChannel(ctx, p)
	},

	"searchMessagesInChannel": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.SearchMessagesInChannel(ctx, p)
	},

	// CHATS
	"createOneOnOneChat": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.CreateOneToOneChat(ctx, p)
	},

	"createGroupChat": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.CreateGroupChat(ctx, p)
	},

	"getChat": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.GetChat(ctx, p)
	},

	"addMemberToGroupChat": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.AddMemberToGroupChat(ctx, p)
	},

	"removeMemberFromGroupChat": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.RemoveMemberFromGroupChat(ctx, p)
	},

	"listMembersInGroupChat": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.ListGroupChatMembers(ctx, p)
	},

	"updateGroupChatTopic": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.UpdateGroupChatTopic(ctx, p)
	},

	"listMessagesInChat": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.ListMessagesInChat(ctx, p)
	},

	"sendMessageInChat": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.SendMessageInChat(ctx, p)
	},

	"deleteMessageInChat": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.DeleteMessageInChat(ctx, p)
	},

	"getMessageInChat": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.GetMessageInChat(ctx, p)
	},

	"listMyChats": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.ListMyChats(ctx, p)
	},

	"listMyChatMessages": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.ListMyChatMessages(ctx, p)
	},

	"listPinnedMessagesInChat": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.ListPinnedMessagesInChat(ctx, p)
	},

	"pinMessageInChat": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.PinMessageInChat(ctx, p)
	},

	"unpinMessageInChat": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.UnpinMessageInChat(ctx, p)
	},

	"getMentionsInChat": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.GetMentionsInChat(ctx, p)
	},

	"searchMessagesInChat": func(c *TeamsJSONClient, ctx context.Context, p map[string]any) (any, error) {
		return c.SearchMessagesInChat(ctx, p)
	},
}
