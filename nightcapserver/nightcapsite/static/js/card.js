const cards = document.querySelectorAll(".card");
// const onDocumentMouseMoveHandler = (evt) => {
//   evt.preventDefault();

//   requestAnimationFrame(() => {
//     if (!evt.target.closest('.card')) {
//       card.style.transform = 'perspective(1000px) scale(1) rotateX(0) rotateY(0)';
//     }
//   });
// };
// document.addEventListener('mousemove', onDocumentMouseMoveHandler)
cards.forEach((card) => {
  const height = card.clientHeight;
  const width = card.clientWidth;

  const mouseMoveHandler = (evt) => {
    evt.preventDefault();

    requestAnimationFrame(() => {
      const xRotation = -30 * ((evt.layerY - height / 2) / height);
      const yRotation = 20 * ((evt.layerX - width / 2) / width);

      card.style.transform = `perspective(1000px) scale(1.05) rotateX(${xRotation}deg) rotateY(${yRotation}deg)`;
    });
  };

  card.addEventListener("mousemove", mouseMoveHandler);

  card.addEventListener("mouseenter", (evt) => {
    evt.preventDefault();
    card.addEventListener("mousemove", mouseMoveHandler);
  });

  card.addEventListener("mouseout", (evt) => {
    evt.preventDefault();
    card.style.transform = "perspective(1000px) scale(1) rotateX(0) rotateY(0)";
    card.removeEventListener("mousemove", mouseMoveHandler);
  });
  
  card.addEventListener("click", (evt) => {
    evt.preventDefault();
    card.style.animation = "spin 1s ease-in-out";
    setTimeout(() => {
      card.style.animation = '';
    }, 1000);
  });
});
