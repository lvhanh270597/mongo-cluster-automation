db = connect("mongodb://localhost:__port__/admin")

db.auth("__user__", "__pass__")

rs.initiate(
    {
      _id: "__replName__",
      members: [
        { _id : 0, host : "__host__" }
      ]
    }
)
