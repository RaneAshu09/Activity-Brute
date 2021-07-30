const express = require("express");
const formidable = require("formidable");
const fs = require("fs");
const cors = require("cors");
const fileUpload = require("express-fileupload");
const spawn = require("cross-spawn");
const path = require("path");

const { convertXMITOJSON } = require("../server1/scripts");

const app = express();

app.use(express.static("public"));
app.use(express.json());
app.use(cors());

app.post("/submit", (req, res) => {
  console.log("route visited");
  let form = new formidable.IncomingForm();
  form.keepExtensions = true;
  form.parse(req, (err, _fields, files) => {
    if (err) {
      return res.status(400).json({
        error: "error in parsing the file",
      });
    }

    if (files.myfile !== undefined) {
      convertXMITOJSON(files.myfile.path)
        .then((result) => {
          return res.status(200).json(result);
        })
        .catch((_err) => console.log("error in getting result!"));
    } else {
      return res.status(400).json({
        error: "error in reading the file",
      });
    }
  });
});

app.get("/", (_req, res) => {
  return res.send("hello world!");
});

app.use(fileUpload());

app.post("/upload", (req, res) => {
  if (fs.existsSync(path.join("./", "myfile.xlsx")))
    fs.unlinkSync(path.join("./", "myfile.xlsx"));

  if (!req.files) {
    return res.status(500).send({ msg: "file is not found" });
  }
  const myFile = req.files.file;
  myFile.name = "myfile.xlsx";
  myFile.mv(`./${myFile.name}`, function (err) {
    if (err) {
      console.log(err);
      return res.status(500).send({ msg: "Error in uploading file" });
    }
    return res.send({ name: myFile.name, path: `/${myFile.name}` });
  });
});

app.post("/Pairs", (req, res) => {
  const data = JSON.stringify(req.body.Data);
  const process = spawn("python", ["../pyScript/Pairs.py", data]);
  process.stdout.on("data", (data) => {
    res.send(data);
  });
});

app.get("/download", (_req, res) => {
  var file = "Final.xlsx";
  var fileLocation = path.join("./", file);
  res.download(fileLocation, file);
});

app.get("/brute", (_req, res) => {
  try {
    if (fs.existsSync(path.join("./", "Final.xlsx")))
      fs.unlinkSync(path.join("./", "Final.xlsx"));

    const process = spawn("python", ["../pyScript/Brute.py"]);

    process.stdout.on("data", (_data) => {});

    process.stdout.on("error", (_data) => {
      res.status(400).send();
    });

    process.stdout.on("end", function () {
      if (fs.existsSync(path.join("./", "Final.xlsx"))) {
        res.status(200).send();
      } else {
        res.status(400).send();
      }
    });
    process.stdin.end();
  } catch (e) {
    res.status(400).send();
  }
});

const port = 8000 || process.env.PORT;

app.listen(port, () => {
  console.log("server is running on port ", port);
});
