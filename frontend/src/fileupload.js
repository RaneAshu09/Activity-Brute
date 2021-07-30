import React, { useRef, useState } from "react";
import axios from "axios";
import { API } from "./backend";
import { Container, Alert } from "react-bootstrap";

function FileUpload() {
  const [values, setValues] = useState({
    error: "",
    success: "",
    dark: true,
    yellow: "",
    up_disabled: true,
    d_disabled: true,
  });

  const { error, success, dark, yellow, up_disabled, d_disabled } = values;
  const [appState, setAppState] = useState("Upload a File");
  const [file, setFile] = useState("");
  const [data, getFile] = useState({ name: "", path: "" });
  const el = useRef();
  let url = `${API}/download`;

  const handleChange = (e) => {
    const file = e.target.files[0];
    setFile(file);
  };

  const uploadFile = () => {
    const formData = new FormData();
    formData.append("file", file);

    axios
      .post(`${API}/upload`, formData, {})
      .then((res) => {
        getFile({
          name: res.data.name,
          path: `${API}/upload` + res.data.path,
        });
        setValues({
          ...values,
          error: "",
          success: true,
          dark: "",
          yellow: "",
          up_disabled: false,
          d_disabled: true,
        });
        setAppState("Success...!! File Uploaded");
      })
      .catch((_err) => {
        setValues({
          ...values,
          error: true,
          success: "",
          dark: "",
          yellow: "",
          up_disabled: true,
          d_disabled: true,
        });
        setAppState("Error...!! File Not Uploaded");
      });
  };

  const fetchBrute = () => {
    setAppState("*** Wait ***");
    setValues({
      ...values,
      error: "",
      success: "",
      dark: "",
      yellow: true,
      up_disabled: true,
      d_disabled: true,
    });

    axios({
      url: `${API}/brute`,
      method: "get",
    })
      .then(function (res) {
        if (res.status === 200) {
          setAppState("Success: Test Case Generated");
          setValues({
            ...values,
            error: "",
            success: true,
            dark: "",
            yellow: "",
            up_disabled: false,
            d_disabled: false,
          });
        } else {
          setAppState("Error: File not Generated");
          setValues({
            ...values,
            error: true,
            success: "",
            dark: "",
            yellow: "",
            up_disabled: false,
            d_disabled: true,
          });
        }
      })
      .catch(function (_error) {
        setAppState("Error: File not Generated");
        setValues({
          ...values,
          error: true,
          success: "",
          dark: "",
          yellow: "",
          up_disabled: false,
          d_disabled: true,
        });
      });
  };

  const download = () => {
    setAppState("File Downloaded");
    setValues({
      ...values,
      error: "",
      success: true,
      dark: "",
      yellow: "",
      up_disabled: false,
      d_disabled: true,
    });
  };

  return (
    <div>
      <br />
      <h1>Test Case Generator</h1>
      <br />
      <div className="container">
        <div className="card border-0 shadow">
          <div className="card-body p-5">
            <div className="file-upload text-center">
              <input
                type="file"
                ref={el}
                onChange={handleChange}
                accept=".xlsx,.csv,.xlxs"
              />
              {"  "}
              <button onClick={uploadFile} className="upbutton btn btn-dark">
                Upload
              </button>
              <br />
              <br />
              {"  "}
              <button
                onClick={fetchBrute}
                className="btn btn-primary"
                disabled={up_disabled}
              >
                Generate Cases
              </button>
              {"  "}
              <br />
              <br />
              <a href={url}>
                {" "}
                <button
                  className="btn btn-success"
                  disabled={d_disabled}
                  onClick={download}
                >
                  Download
                </button>
              </a>
            </div>
          </div>

          <Container fluid>
            {error && (
              <Alert variant="danger">
                <h1 className="text-center">{appState}</h1>
              </Alert>
            )}
            {success && (
              <Alert variant="success">
                <h1 className="text-center">{appState}</h1>
              </Alert>
            )}
            {dark && (
              <Alert variant="dark">
                <h1 className="text-center">{appState}</h1>
              </Alert>
            )}
            {yellow && (
              <Alert variant="warning">
                <h1 className="text-center">{appState}</h1>
              </Alert>
            )}
          </Container>
        </div>
        <br />

        <div className="card border-0 shadow my-5">
          <div className="card-body p-5">
            <h4 className="text-center">Process</h4>
            <h6>1.Upload the excel file</h6>
            <h6>2.Click on generate test cases PSO/TLBO/SA</h6>
            <h6>3.Once uploaded sucessfully, test cases will be generated</h6>
            <h6>4.Download the text file of generated test cases</h6>
          </div>
        </div>
      </div>
    </div>
  );
}
export default FileUpload;
