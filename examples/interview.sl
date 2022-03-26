(fun split in delim:
  (fun impl in delim chunk:
    (if in
      (let h (head in));
      (let t (tail in));
      (if (== h delim)
        (push chunk (impl t delim ""))
        (impl t delim (+ chunk h))
      )
      [chunk]
    )
  );
  (impl in delim "")
);
(fun trim in:
  (if in
    (let h (head in));
    (let t (tail in));
    (if (== h " ")
      (trim t)
      (+ h (trim t))
    )
    ""
  )
);
(fun map f l:
  (if l
    (push (f (head l)) (map f (tail l)))
    []
  )
);
(fun in e l:
  (if l
    (let h (head l));
    (let t (tail l));
    (if (== e h)
      True
      (in e t)
    )
    False
  )
);
(fun filter p l:
  (if l
    (let h (head l));
    (let t (tail l));
    (if (p h)
      (push h (filter p t))
      (filter p t)
    )
    []
  )
);
(fun find_supported client server:
  (filter (fun supported e:
    (in e server)
  ) (map trim (split client ",")))
);
(find_supported "a-x, b-y" ["b-y" "a-x"])