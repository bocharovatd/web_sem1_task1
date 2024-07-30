const searchInput = document.getElementById('search-input');
const suggestionsContainer = document.getElementById('search-suggestions');
let timeoutId;

searchInput.addEventListener('input', () => {
    clearTimeout(timeoutId);
    const searchTerm = searchInput.value.trim();
    timeoutId = setTimeout(async () => {
        if (searchTerm) {
            try {
                const response = await fetch(`/search/suggestions/?q=${searchTerm}`);
                const data = await response.json();
                suggestionsContainer.innerHTML = '';
                JSON.parse(data).forEach(result => {
                    const suggestionLi = document.createElement('li');
                    const suggestionA = document.createElement('a');
                    suggestionA.classList.add('dropdown-item');
                    suggestionA.href = `/questions/${result.pk}`;
                    suggestionA.innerText = result.fields.title;
                    suggestionLi.appendChild(suggestionA);
                    suggestionsContainer.appendChild(suggestionLi);
                });
            } catch (error) {
                console.error('Error in getting data:', error);
            }
        } else {
            suggestionsContainer.innerHTML = '';
        }
    }, 500); // Задержка в 500 мс
});

// без таймера

// const searchInput = document.getElementById('search-input');
// const suggestionsContainer = document.getElementById('search-suggestions');
// // console.log(searchInput);
// // let timeoutId = null; // Для отмены предыдущих запросов
//
// searchInput.addEventListener('input', async () => {
//     const searchTerm = searchInput.value.trim();
//     fetch(`/search/suggestions/?q=${searchTerm}`)
//         .then(response => response.json())
//         .then(data => {
//             suggestionsContainer.innerHTML = '';
//             JSON.parse(data).forEach(result => {
//                 const suggestionLi = document.createElement('li');
//                 const suggestionA = document.createElement('a');
//                 suggestionA.classList.add('dropdown-item');
//                 suggestionA.href = `/questions/${result.pk}`;
//                 suggestionA.innerText = result.fields.title;
//                 suggestionLi.appendChild(suggestionA);
//                 suggestionsContainer.appendChild(suggestionLi);
//             })
//         });
// });