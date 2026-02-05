import "../../styles/App.css";
import Arrow from "../../assets/img/up.svg";
import Check from "../../assets/img/check.svg";
import Button from "../../components/button";
import BoxUpload from "../../components/box";
// import { useEffect, useState } from "react";
import { useImageProcessor } from "../../hooks/imageProcessor";
import ResultDisplay from "../../components/result";

const HomePage = () => {
  const {
    image1,
    setImage1,
    image2,
    setImage2,
    result,
    loading,
    error,
    processImages,
    reset,
  } = useImageProcessor();

  const isButtonActive = image1.length > 0 && image2.length > 0 && !loading;

  return (
    <div className="home">
      {!result ? (
        <>
          <header className="home__text">
            <h2>Upload your images</h2>
            <p>Upload images to process them through our algorithm.</p>
          </header>
          <div className="home__container">
            <BoxUpload
              status={image1.length > 0}
              img={image1.length === 0 ? Arrow : Check}
              headline="Cropped Image"
              onFileSelect={setImage1}
            />
            <BoxUpload
              multiple
              status={image2.length > 0}
              img={image2.length === 0 ? Arrow : Check}
              headline="Reference Image"
              onFileSelect={setImage2}
            />
          </div>
        </>
      ) : (
        <ResultDisplay result={result} />
      )}

      {error && <div className="error">{error}</div>}

      {!result ? (
        <Button
          text={loading ? "Processing..." : "Process image"}
          active={isButtonActive}
          onClick={processImages}
        />
      ) : (
        <Button text="Back to homepage" active={true} onClick={reset} />
      )}
    </div>
  );
};

export default HomePage;
