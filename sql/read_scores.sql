SELECT sc.timestamp,
       sc.name,
       sc.easy,
       sc.medium,
       sc.hard
  FROM scores sc
  JOIN (SELECT MAX(scr.timestamp) 'maxtimestamp'
         FROM scores scr
     GROUP BY date(scr.timestamp)) m ON m.maxtimestamp = sc.timestamp;