import React, { useState } from "react";
import axios from "axios";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleFileUpload = async () => {
    if (!selectedFile) {
      setUploadStatus("Por favor, selecione um arquivo.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await axios.post("/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setUploadStatus("Upload bem-sucedido! Arquivo processado.");
      console.log(response.data);
    } catch (error) {
      setUploadStatus("Erro no upload.");
      console.error("Erro no upload:", error);
    }
  };

  return (
    <div className="App">
      <h1>Carregar Arquivo GeoJSON, KMZ ou SHP</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleFileUpload}>Enviar</button>
      <p>{uploadStatus}</p>
    </div>
  );
}

export default App;
