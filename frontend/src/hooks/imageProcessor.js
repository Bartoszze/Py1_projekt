import { useState } from "react";

export const useImageProcessor = () => {
  const [image1, setImage1] = useState([]);
  const [image2, setImage2] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const reset = () => {
    setImage1([]);
    setImage2([]);
    setResult(null);
    setError(null);
  };

  const processImages = async () => {
    if (image1.length === 0 || image2.length === 0) {
      setError("Files not found");
      return;
    }

    if (
      image1[0]?.name === image2[0]?.name &&
      image1[0]?.size === image2[0]?.size
    ) {
      setError("Please select two different images.");
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("obraz1", image1[0]);
    formData.append("obraz2", image2[0]);

    try {
      const response = await fetch("http://127.0.0.1:5000/api/przetworz", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.Error || "Server error");
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return {
    image1,
    setImage1,
    image2,
    setImage2,
    result,
    loading,
    error,
    processImages,
    reset,
  };
};
