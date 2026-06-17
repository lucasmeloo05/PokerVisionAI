import { useState, useRef } from "react";
import axios from "axios";
import "./App.css";
import { useEffect } from "react";

function App() {


  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);

  const [cameraOn, setCameraOn] = useState(false);
  const [stream, setStream] = useState(null);

  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {

    if (
      cameraOn &&
      stream &&
      videoRef.current
    ) {
      videoRef.current.srcObject = stream;
    }

  }, [cameraOn, stream]);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];

    if (!selectedFile) return;

    setFile(selectedFile);
    setPreview(URL.createObjectURL(selectedFile));
  };

  const saveHistory = (data) => {
    if (data.cards.length > 0) {
      setHistory((old) => [
        {
          cards: data.cards.join(", "),
          hand: data.hand,
        },
        ...old,
      ]);
    }
  };

  const sendImage = async () => {
    if (!file) return;

    const formData = new FormData();

    formData.append("file", file);

    try {
      const response = await axios.post(
        "http://localhost:8000/predict",
        formData
      );

      setResult(response.data);

      saveHistory(response.data);

    } catch (error) {
      console.error(error);
      alert("Erro ao conectar com a API");
    }
  };

  const startCamera = async () => {
    try {

      const mediaStream =
        await navigator.mediaDevices.getUserMedia({
          video: true
        });

      setStream(mediaStream);
      setCameraOn(true);

    } catch (error) {

      console.error(error);

      alert(
        "Não foi possível acessar a webcam."
      );
    }
  };

  const stopCamera = () => {

    if (videoRef.current?.srcObject) {

      const mediaStream = videoRef.current.srcObject;

      mediaStream
        .getTracks()
        .forEach((track) => track.stop());

      videoRef.current.srcObject = null;
    }

    setStream(null);
    setCameraOn(false);
  };

  const capturePhoto = async () => {
    const canvas = canvasRef.current;

    const video = videoRef.current;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");

    ctx.drawImage(
      video,
      0,
      0,
      canvas.width,
      canvas.height
    );

    canvas.toBlob(async (blob) => {
      try {

        const formData = new FormData();

        formData.append(
          "file",
          blob,
          "webcam.jpg"
        );

        const response = await axios.post(
          "http://localhost:8000/predict",
          formData
        );

        setResult(response.data);

        saveHistory(response.data);

      } catch (error) {
        console.error(error);
        alert("Erro ao conectar com a API");
      }
    }, "image/jpeg");
  };

  return (
    <div className="container">

      <h1>🃏 PokerVisionAI</h1>

      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
      />

      {preview && (
        <div className="preview">
          <img
            src={preview}
            alt="Preview"
            width="300"
          />
        </div>
      )}

      <button onClick={sendImage}>
        Analisar Imagem
      </button>

      <br />
      <br />

      <button onClick={startCamera}>
        Abrir Webcam
      </button>

      <button
        onClick={stopCamera}
        style={{ marginLeft: "10px" }}
      >
        Fechar Webcam
      </button>

      {cameraOn && (
        <div style={{ marginTop: "20px" }}>

          <video
            ref={videoRef}
            autoPlay
            width="500"
            style={{
              borderRadius: "10px",
              border: "2px solid white"
            }}
          />

          <br />

          <button
            onClick={capturePhoto}
            style={{
              marginTop: "10px"
            }}
          >
            Capturar e Analisar
          </button>

          <canvas
            ref={canvasRef}
            style={{
              display: "none"
            }}
          />

        </div>
      )}

      {result && result.cards.length > 0 && (
        <div className="result">

          <h2>Cartas Detectadas</h2>

          <div className="cards-container">

            {result.cards.map((card) => {

              const rank = card.slice(0, -1);
              const suit = card.slice(-1);

              const symbols = {
                H: "♥",
                D: "♦",
                S: "♠",
                C: "♣"
              };

              return (
                <div
                  key={card}
                  className={`card ${
                    suit === "H" || suit === "D"
                      ? "red"
                      : "black"
                  }`}
                >
                  {rank}
                  {symbols[suit]}
                </div>
              );
            })}

          </div>

          <h2>Mão Identificada</h2>
          <p>{result.hand}</p>

          <h2>Força da Mão</h2>

          <div className="strength-bar">
            <div
              className="strength-fill"
              style={{
                width: `${result.strength}%`
              }}
            />
          </div>

          <p>{result.strength}/100</p>

          <h2>Recomendação</h2>
          <p>{result.recommendation}</p>

        </div>
      )}

      {result && result.cards.length === 0 && (
        <div className="result">
          <h2>Nenhuma carta detectada</h2>
        </div>
      )}

      {history.length > 0 && (
        <div className="history">

          <h2>Histórico</h2>

          {history.map((item, index) => (
            <div
              key={index}
              style={{
                marginBottom: "10px",
                padding: "10px",
                border: "1px solid #ccc",
                borderRadius: "8px",
              }}
            >
              <strong>Cartas:</strong> {item.cards}
              <br />
              <strong>Mão:</strong> {item.hand}
            </div>
          ))}

        </div>
      )}

    </div>
  );
}

export default App;