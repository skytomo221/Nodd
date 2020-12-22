require 'discordrb'
bot = Discordrb::Bot.new token: 'token'

member_number = 0

bot.message(content: 'hello') do |event|
  event.respond "#{event.user.name}:こんにちは"
end

bot.ready do |event|
  bot.servers.each_value do |srv|
    srv.users.each do |user|
      bot.send_message(CHANNEL_OBJECT, "#{user.name}:こんにちは")
    end
  end
  print "OK"
end

bot.run
