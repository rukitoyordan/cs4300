Feature: Book an available movie seat
  Scenario: A signed-in customer reserves a seat
    Given a movie has an available seat
    And I am signed in as a customer
    When I book that seat
    Then I am redirected to my booking history
    And my booking history shows the movie and seat
