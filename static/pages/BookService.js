const BookService = {
    template: `
      <div>
        <h1>Book a Service</h1>
        <form>
          <div class="form-group">
            <label for="service">Select Service</label>
            <select id="service" class="form-control">
              <option>Cleaning</option>
              <option>Plumbing</option>
              <option>Electrical</option>
            </select>
          </div>
          <div class="form-group">
            <label for="date">Select Date</label>
            <input type="date" id="date" class="form-control"/>
          </div>
          <button type="submit" class="btn btn-primary">Book Now</button>
        </form>
      </div>
    `,
  };
  
  export default BookService;
  