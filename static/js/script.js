document.getElementById('uploadForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const formData = new FormData(this); // Automatically includes file and difficulty
    const loadingDiv = document.getElementById('loading'); // Show loading indicator
    loadingDiv.style.display = 'block';

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            loadingDiv.style.display = 'none';
            if (data.questions) {
                displayQuestions(data.questions);
            } else if (data.error) {
                alert(data.error);
            }
        })
        .catch(error => {
            loadingDiv.style.display = 'none';
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
});

function displayQuestions(questions) {
    const questionsList = document.getElementById("questions-list");
    questionsList.innerHTML = ""; // Clear previous questions

    if (questions.length > 0) {
        questions.forEach((question, index) => {
            const listItem = document.createElement("li");
            listItem.textContent = `Q${index + 1}: ${question}`;
            questionsList.appendChild(listItem);
        });
    } else {
        questionsList.innerHTML = "<li>No questions generated.</li>";
    }
}

// Assuming you have a button or an event that triggers the upload or action
document.getElementById('uploadButton').addEventListener('click', function() {
    // Add 'active' class to the question-output container when the upload button is pressed
    document.querySelector('.question-output').classList.add('active');
});
