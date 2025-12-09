const Button = ({ text, srcImg, altImg, onClick, href, active }) => {
  const buttonColor = {
    backgroundColor: active ? "#2476FF" : "#C8E0FF",
  };
  return (
    <a className="custom-link" href={href} rel="noreferrer" onClick={onClick}>
      <button style={buttonColor} className="custom-button">
        {text}
      </button>
      <img src={srcImg} alt={altImg} />
    </a>
  );
};

export default Button;
