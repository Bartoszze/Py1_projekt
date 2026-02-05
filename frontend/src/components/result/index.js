const ResultDisplay = ({ result }) => {
  if (!result || !result.result) return null;

  return (
    <div className="animation">
      <h2>Processing Result:</h2>
      <p>
        Number of matches: <span>{result.matches}</span>
      </p>
      <img
        src={`data:image/png;base64,${result.result}`}
        alt="Wynik dopasowania"
        style={{ maxWidth: "100%", border: "1px solid #ddd" }}
      />
      <p className="home__results--gemini">{result.geoInfo}</p>
    </div>
  );
};

export default ResultDisplay;
