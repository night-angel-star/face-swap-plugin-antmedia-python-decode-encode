const http = require("http");
const fs = require("fs");

let num = 1;

const server = http.createServer((req, res) => {
  if (req.method === "POST") {
    let body = "";

    req.on("data", (chunk) => {
      body += chunk.toString();
    });

    req.on("end", () => {
      try {
        const currentDate = new Date();
        const year = currentDate.getFullYear();
        const month = String(currentDate.getMonth() + 1).padStart(2, "0");
        const day = String(currentDate.getDate()).padStart(2, "0");
        const hours = String(currentDate.getHours()).padStart(2, "0");
        const minutes = String(currentDate.getMinutes()).padStart(2, "0");
        const seconds = String(currentDate.getSeconds()).padStart(2, "0");
        const milliseconds = String(currentDate.getMilliseconds()).padStart(
          3,
          "0"
        );

        const currentTime = `${year}${month}${day}_${hours}${minutes}${seconds}_${milliseconds}`;
        fs.writeFileSync(`./frames/${currentTime}.dat`, body + "\n");
        const receivedData = JSON.parse(body);
        console.log(
          currentTime,
          receivedData.height,
          receivedData.width,
          receivedData.format
        );

        fs.readFile(`output${num}.dat`, "utf8", (err, data) => {
          if (err) {
            console.error(err);
            return;
          }

          res.writeHead(200, { "Content-Type": "application/text" });
          res.end(data);
          num = 1 ? 2 : 1;
        });

        // res.writeHead(200, { "Content-Type": "application/text" });
        // res.end(receivedData.data);
      } catch (error) {
        console.log(error);
        res.writeHead(400, { "Content-Type": "text/plain" });
        res.end("Invalid JSON payload");
      }
    });
  } else {
    res.writeHead(404, { "Content-Type": "text/plain" });
    res.end("Not Found");
  }
});

const PORT = 5000;
server.listen(PORT, () => {
  console.log(`Server is running at http://localhost:${PORT}`);
});
