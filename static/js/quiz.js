document.addEventListener("DOMContentLoaded", () => {
  let currentIndex = 0;
  let userAnswers = new Array(quizData.length).fill(null);

  const qNumber = document.getElementById("q-number");
  const qText = document.getElementById("q-text");
  const optionsDiv = document.getElementById("options");
  const progress = document.getElementById("progress");
  const navigatorDiv = document.getElementById("navigator");

  const nextBtn = document.getElementById("nextBtn");
  const prevBtn = document.getElementById("prevBtn");
  const submitBtn = document.getElementById("submitBtn");

  function renderQuestion() {
    const q = quizData[currentIndex];

    qNumber.innerText = `Question ${currentIndex + 1}`;
    qText.innerText = q.question;

    optionsDiv.innerHTML = "";
    q.options.forEach((opt, idx) => {
      const div = document.createElement("div");
      div.className = "option-box";
      if (userAnswers[currentIndex] === idx) div.classList.add("selected");

      div.innerText = opt;
      div.onclick = () => {
        userAnswers[currentIndex] = idx;
        renderQuestion();
        renderNavigator();
      };

      optionsDiv.appendChild(div);
    });

    progress.innerText =
      `${userAnswers.filter(a => a !== null).length} of ${quizData.length} answered`;

    updateButtons();
  }

  function renderNavigator() {
    navigatorDiv.innerHTML = "";
    quizData.forEach((_, i) => {
      const box = document.createElement("div");
      box.className = "nav-item";
      if (i === currentIndex) box.classList.add("active");
      if (userAnswers[i] !== null) box.classList.add("answered");

      box.innerText = i + 1;
      box.onclick = () => {
        currentIndex = i;
        renderQuestion();
        renderNavigator();
      };

      navigatorDiv.appendChild(box);
    });
  }

  function updateButtons() {
    prevBtn.disabled = currentIndex === 0;
  }

  nextBtn.onclick = () => {
    if (currentIndex < quizData.length - 1) {
      currentIndex++;
      renderQuestion();
      renderNavigator();
    }
  };

  prevBtn.onclick = () => {
    if (currentIndex > 0) {
      currentIndex--;
      renderQuestion();
      renderNavigator();
    }
  };

  submitBtn.onclick = () => {
    const payload = quizData.map((q, i) => ({
      question: q.question,
      options: q.options,
      correct_answer: q.options[q.answer],
      user_answer:
        userAnswers[i] !== null ? q.options[userAnswers[i]] : null
    }));

    document.getElementById("answersInput").value =
      JSON.stringify(payload);

    document.getElementById("resultForm").submit();
  };

  renderQuestion();
  renderNavigator();
});
