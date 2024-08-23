document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');
    document.getElementById('search-form').addEventListener('submit', function(e) {
        console.log('Form submitted');
        e.preventDefault();
        searchCountry();
    });
});

function searchCountry() {
    console.log('searchCountry function called');
    const country = document.getElementById("country-search").value.toUpperCase();
   
    console.log(`Fetching data for country: ${country}`);
   
    fetch(`http://127.0.0.1:5000/api/payout-partners?country=${country}`)
        .then(response => {
            return response;
            // console.log('Response status:', response.status);
            // console.log('Response headers:', response.headers);
            // return response.json();  // Get the raw text of the response
        })
        .then(data => {
            console.log('Data received:', data);
            if (Array.isArray(data)) {
                populateDropdown(data);  // Call function to populate dropdown with the array of objects
            } else {
                console.error('Expected an array but received:', data);
                alert('Unexpected data format received.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while fetching data: ' + error.message);
        });
}


function displayPartners(partners) {
    const partnersList = document.getElementById('partners-list');
    partnersList.innerHTML = '<h2>Payout Partners</h2>';
   
    partners.forEach((partner, index) => {
        const partnerItem = document.createElement('div');
        partnerItem.className = 'list-item';
        partnerItem.textContent = `${index + 1}. ${partner.name}`;
        partnerItem.onclick = () => getCities(partner.guid);
        partnersList.appendChild(partnerItem);
    });

    document.getElementById('results-container').style.display = 'block';
    document.getElementById('cities-list').style.display = 'none';
    document.getElementById('locations-list').style.display = 'none';
}

function getCities(partnerGuid) {
    const country = document.getElementById("country-search").value.toUpperCase();
   
    fetch(`/api/payout-locations?country=${country}&partner_guid=${partnerGuid}`)
        .then(response => response.json())
        .then(data => {
            displayCities(data, partnerGuid);
        });
}

function displayCities(cities, partnerGuid) {
    const citiesList = document.getElementById('cities-list');
    citiesList.innerHTML = '<h2>Cities</h2>';
   
    cities.forEach((city, index) => {
        const cityItem = document.createElement('div');
        cityItem.className = 'list-item';
        cityItem.textContent = `${index + 1}. ${city}`;
        cityItem.onclick = () => getLocations(partnerGuid, city);
        citiesList.appendChild(cityItem);
    });

    citiesList.style.display = 'block';
    document.getElementById('locations-list').style.display = 'none';
}

function getLocations(partnerGuid, city) {
    const country = document.getElementById("country-search").value.toUpperCase();
   
    fetch(`/api/payout-locations?country=${country}&partner_guid=${partnerGuid}&city=${encodeURIComponent(city)}`)
        .then(response => response.json())
        .then(data => {
            displayLocations(data);
        });
}

function displayLocations(locations) {
    const locationsList = document.getElementById('locations-list');
    locationsList.innerHTML = '<h2>Payout Locations</h2>';
   
    locations.forEach((location, index) => {
        const locationItem = document.createElement('div');
        locationItem.className = 'list-item';
        locationItem.innerHTML = `
            <h3>${index + 1}. ${location.name}</h3>
            <div class="location-details">
                <p>Address: ${location.address}</p>
                <p>Coordinates: ${location.coordinates}</p>
                <p>Currencies: ${location.currencies}</p>
            </div>
        `;
        locationsList.appendChild(locationItem);
    });

    locationsList.style.display = 'block';
}

function populateDropdown(items) {
    const dropdown = document.getElementById('dropdown-id');  // Replace with your dropdown ID
    dropdown.innerHTML = '';  // Clear existing options

    items.forEach(item => {
        const option = document.createElement('option');
        option.value = item.guid;  // or whatever value you need
        option.textContent = item.name;
        dropdown.appendChild(option);
    });
}