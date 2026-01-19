import "../../styles/App.css";
import Arrow from "../../assets/img/up.svg";
import Check from "../../assets/img/check.svg";
import Button from "../../components/button";
import BoxUpload from "../../components/box";
import { useEffect, useState } from "react";

function HomePage() {
  const [image1, setImage1] = useState([]);
  const [image2, setImage2] = useState([]);
  const [result, setResult] = useState(null);
  const [buttonStatus, setButtonStatus] = useState(false);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileSelected1 = (file) => {
    setImage1(file);
  };
  const handleFileSelected2 = (file) => {
    setImage2(file);
  };
  const handleReset = () => {
    setImage1([]);
    setImage2([]);
    setResult(null);
    setError(null);
  };
  const handleProcessButton = async () => {
    if (image1 == null || image2 == null) {
      setError("Files not found");
    } else {
      if (
        image1[0]?.name === image2[0]?.name &&
        image1[0]?.size === image2[0]?.size
      ) {
        console.log(image2);
        setError(
          "Please select two different images (they must not be the same file).",
        );
      } else {
        console.log(image1[0].type, image2);
        setLoading(true);
        setError(null);
        setResult(null);
        const formData = new FormData();
        image1.forEach((file) => {
          formData.append("obraz1", file);
        });
        image2.forEach((file) => {
          formData.append("obraz2", file);
        });

        try {
          const response = await fetch("http://127.0.0.1:5000/api/przetworz", {
            method: "POST",
            body: formData,
          });

          const data = await response.json();

          if (!response.ok) {
            throw new Error(data.Błąd || data.błąd || `${data.Error}`);
          }
          setResult(data);
        } catch (err) {
          setError(err.message);
          console.error("Wystąpił błąd:", err.message);
        } finally {
          setLoading(false);
        }
      }
    }
  };

  useEffect(() => {
    // console.log(image1.length === 0, image2);
    setButtonStatus(image1.length !== 0 && image2.length !== 0);
  }, [image1, image2]);

  return (
    <div className="home">
      {!result && (
        <>
          <div className="home__text">
            <h2>Upload your images</h2>
            <p>
              Upload one image to process it through our advanced algorithm and
              get a quick result.
            </p>
          </div>
          <div className="home__container">
            <BoxUpload
              status={image1.length === 0 ? false : true}
              img={image1.length === 0 ? Arrow : Check}
              headline="Cropped Image"
              onFileSelect={handleFileSelected1}
            />
            <BoxUpload
              multiple
              status={image2.length === 0 ? false : true}
              img={image2.length === 0 ? Arrow : Check}
              headline="Reference Image"
              onFileSelect={handleFileSelected2}
            />
          </div>
        </>
      )}

      <div
        className="home__results"
        // style={{ marginTop: "20px", width: "100%" }}
      >
        {error && (
          <div className="error" style={{ color: "red", fontWeight: "bold" }}>
            {error}
          </div>
        )}
        {result && result.result && (
          <div className="animation">
            <h2>Processing Result: </h2>
            {/* <p className="home__results--gemini">{result.geoInfo}</p> */}
            <p>
              Number of matches: <span>{result.matches} </span>
            </p>
            <img
              src={`data:image/png;base64,${result.result}`}
              alt="Wynik dopasowania"
              style={{ maxWidth: "100%", border: "1px solid #ddd" }}
            />
            <p className="home__results--gemini">{result.geoInfo}</p>
          </div>
        )}
      </div>
      {!result && (
        <Button
          text={loading ? "Processing..." : "Process image"}
          active={buttonStatus && !loading}
          onClick={handleProcessButton}
        />
      )}
      {result !== null && (
        <Button text="Back to homepage" active={true} onClick={handleReset} />
      )}
    </div>
  );
}

export default HomePage;
