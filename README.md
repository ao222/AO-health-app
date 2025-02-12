# AO-health-app

## TODO
1. Refactor Food Snapshots to mimick objective and subjective snapshot database models (from a document for each day to just one collections, i.e. flattening the database structure out a bit)
2. Refactor the UTC to local time conversions to a simpler form (ie only save the local time in the database)
3. Add daily reviews for each snapshot (create a class that takes a collections reference and displays today's documents), (allow deletions on today's records)
4. Add a configuration page for local time zone, and current user.
