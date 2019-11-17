db = connect("mongodb://localhost:27017/admin")

db.auth("admin", "password")

rs.initiate(
    {
      _id: "auto_repl",
      members: [
        { _id : 0, host : "172.16.176.130" }
      ]
    }
)
