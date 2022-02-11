Which relations have natural keys?
Theaters: Name Capacity
Screenings: Theater name Movie Start time
Movies: IMDB-key, Title Year
Customers: Username, Password
Tickets: UUID


Is there a risk that any of the natural keys will ever change?
Can't think of anything right now
Are there any weak entity sets?


In which relations do you want to use an invented key, why?

In screenings, using an invented key would be nice because the theater name and movie name might be similar, e.g. Spegeln in Malmö. Also it is quite long with many attributes.



underscores for primary keys
slashes for foreign keys
underscores and slashes for attributes which are both (parts of) primary keys and foreign keys

Theaters (_theater_name_, _Capacity_)
Screenings (/_theater_name_/, /movie/, start_time)
Movies (_IMDB_key_, title, year, runtime)
Customers (_Username_, customer_name, password)
Tickets (_ticketnumber_, /username/, /screening/, /movie/)

There are at least two ways of keeping track of the number of seats available for each performance – describe them both, with their upsides and downsides (write your answer in lab2-answers.md).

Event sourcing, saving history of all tickets sold, calculating number of seats available each time a new ticket is purchased. Saving history allows us to track and explain the current state.
Using a COUNT() to count the number of tickets sold to a screen each time someone tries to purchase a ticket. Easier to keep track of however it needs to recalculate it each time someone buys a ticket. Also no historical evidence that tickets were purchased.

