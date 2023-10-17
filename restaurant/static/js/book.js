// Includes code for DOM manipulation of book.html

// TODO: Fix the hardcoded url values of fetch API

function getBookings() {
  /**
   * Fetch current list of bookings from database using
   * JavaScript fetch API. Based on bookings populate the
   * innerHTML of reservation date and time HTML tags
   */
  let reserved_slots = [];
  const date = document.getElementById("reservation_date").value;
  document.getElementById("today").innerHTML = date;

  // fetch bookings from database
  fetch("http://127.0.0.1:8000/bookings/" + "?date=" + date)
    .then((response) => response.json())
    .then((data) => {
      reserved_slots = [];
      bookings = "";

      for (const item of data) {
        // push value of every reservation_slot field from JSON object
        // returned by database into reserved_slot array
        reserved_slots.push(item.fields.reservation_slot);

        // create HTML paragraph tags dynamically, contains information
        // about the bookings
        bookings += `<p>${item.fields.first_name} - ${formatTime(
          item.fields.reservation_slot
        )}</p>`;
      }

      // create option HTML tag dynamically for reservation slot value
      slot_options = '<option value="0" disabled>Select time</option>';
      // create 10 options for reservation slot; from 10AM to
      // if there is already reserved slot, create option tag
      // but with attribute disabled.
      for (let i = 10; i < 20; i++) {
        // formate integer value into time
        const label = formatTime(i);
        if (reserved_slots.includes(i)) {
          slot_options += `<option value=${i} disabled>${label}</option>`;
        } else {
          slot_options += `<option value=${i}>${label}</option>`;
        }
      }

      // assign slot options to HTML options tag with id reservation_slot
      document.getElementById("reservation_slot").innerHTML = slot_options;

      // if there are not bookings on the current date
      if (bookings === "") {
        bookings = "No bookings";
      }
      // change value of HTML tag with bookings id
      document.getElementById("bookings").innerHTML = bookings;
    });
}

// function to format time based on provided integer value
function formatTime(time) {
  /**
   * Convert integer value into time representation
   * such as 11 -> 11 AM
   */
  const ampm = time < 12 ? "AM" : "PM";
  const t = time < 12 ? time : time > 12 ? time - 12 : time;
  const label = `${t} ${ampm}`;
  return label;
}

// create a new date object and assign its value to HTML tag with
// reservation_date id
const date = new Date();
reservationDate = document.getElementById("reservation_date");
reservationDate.value = `${date.getFullYear()}-${date.getMonth() + 1}-${date
  .getDate()
  .toString()
  .padStart(2, "0")}`;

// get list of bookings
getBookings();

// call getBookings method whenever HTML tag with id reservation_date
// value is changed
document
  .getElementById("reservation_date")
  .addEventListener("change", getBookings);

// submit POST request to server via Reserve button
document.getElementById("button").addEventListener("click", function (e) {
  // get the form data
  const formData = {
    first_name: document.getElementById("first_name").value,
    reservation_date: document.getElementById("reservation_date").value,
    reservation_slot: document.getElementById("reservation_slot").value,
  };

  // submit POST request and refresh bookings data.
  fetch("http://127.0.0.1:8000/bookings/", {
    method: "post",
    body: JSON.stringify(formData),
  })
    .then((response) => response.text())
    .then((data) => {
      getBookings();
    });
});
