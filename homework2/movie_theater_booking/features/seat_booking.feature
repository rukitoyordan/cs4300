Feature: Book an available movie seat
  Scenario: A signed-in customer reserves a seat
    Given a movie has an available seat
    And I am signed in as a customer
    When I book that seat
    Then I am redirected to my booking history
    And my booking history shows the movie and seat

  Scenario: Cannot book a seat that is already taken
    Given a movie has an available seat
    And the seat is already booked by another user
    And I am signed in as a customer
    When I book that seat
    Then I see an error that the seat is unavailable
    And no new booking is created
