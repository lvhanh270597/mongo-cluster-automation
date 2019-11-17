db = connect("mongodb://localhost:__port__/admin")

db.createUser({ user: "__user__", pwd: "__pass__", roles: [
    { role: "userAdminAnyDatabase", db: "admin" },
    { role: "readWriteAnyDatabase", db: "admin" },
    { role: "dbAdminAnyDatabase", db: "admin" },
    { role: "clusterAdmin", db: "admin" }
 ]})