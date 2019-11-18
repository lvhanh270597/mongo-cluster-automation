db = connect("mongodb://localhost:__port__/admin")
db.auth("__user__", "__pass__")

hosts = __list_hosts__
for (var i=0; i<hosts.length; i++){
  rs.add({_id: i + 1, host: hosts[i]})
}