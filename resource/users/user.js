db = connect("mongodb://localhost:__port__/__db__")

db.createUser({ user: "__user__", pwd: "__pass__", roles: [
    { role: "readWrite", db: "__db__" },
 ]})