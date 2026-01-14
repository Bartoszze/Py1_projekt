import { useRef, useState } from "react";

const BoxUpload = ({
  img,
  headline,
  onFileSelect,
  status,
  key,
  multiple = false,
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const handleBoxClick = () => {
    fileInputRef.current.click();
  };
  const handleFileChange = (event) => {
    const file = event.target.files;
    if (file && onFileSelect) {
      const filesArray = Array.from(file);
      onFileSelect(filesArray);
    }
  };
  const handleDragOver = (event) => {
    event.preventDefault();
    setIsDragging(true);
  };
  const handleDragLeave = (event) => {
    event.preventDefault();
    setIsDragging(false);
  };
  const handleDrop = (event) => {
    event.preventDefault(); //bloka otwarcia pliku w nowej karcie
    event.stopPropagation();
    setIsDragging(false);
    const files = event.dataTransfer.files;

    if (files && files.length > 0 && onFileSelect) {
      onFileSelect(files);
    }
  };
  return (
    <div
      className={`home__upload ${status || isDragging ? "active" : ""}`}
      onClick={handleBoxClick}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      key={key}
    >
      <input
        multiple={multiple}
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        style={{ display: "none" }}
        accept="image/png, image/jpeg, image/gif"
      />
      <div className="home__upload--text">
        <h3>{headline}</h3>
      </div>
      <div className="home__upload--box">
        <div className="home__upload--dragDragBox">
          <img src={img} alt="arrowBox" key={img} />
          {!status && (
            <>
              <h4>Click to upload</h4>
              <p>or drag and drop</p>
              <h5>PNG,JPG, GIF up to 100MB </h5>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default BoxUpload;
