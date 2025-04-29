const jwt = require("jsonwebtoken")

exports.handler = async(event)=>{
    const password = event.password
    const hashedPassword = jwt.sign({password},"your_sec_key");
    return{
        statuscode:200,
        body:JSON.stringify({hashedPassword})
    }
}