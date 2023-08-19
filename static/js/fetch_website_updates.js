// static/js/fetch_website_updates.js
function fetchAndDisplayUpdates() {
  fetch('/patch_notes/website_updates')
    .then(response => response.json())
    .then(data => {
      const updatesList = document.getElementById('updates-list');
      updatesList.innerHTML = ''; // Clear previous content

      data.forEach(commit => {
        const card = document.createElement('div');
        card.classList.add('col-md-4', 'mb-4');

        card.innerHTML = `
          <div class="card">
            <div class="card-header">
              <h5 class="card-title">${commit.author}</h5>
              <small class="text-muted">${commit.date}</small>
            </div>
            <div class="card-body">
              <p class="card-text">${commit.message}</p>
            </div>
          </div>
        `;

        updatesList.appendChild(card);
      });
    })
    .catch(error => {
      console.error('Error fetching updates:', error);
    });
}

// Fetch and display updates immediately and then every 2 minutes
fetchAndDisplayUpdates();
setInterval(fetchAndDisplayUpdates, 120000); // 2 minutes in milliseconds
