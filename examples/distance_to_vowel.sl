(let vowels ["a" "e" "i" "o" "u"]);
(fun is_vowel c:
  (fun helper v:
    (if v
      (let h (head v));
      (let t (tail v));
      (if (== c h)
        True
        (helper t)
      )
      False
    )
  );
  (helper vowels)
);
(fun len l:
  (if l
    (+ 1 (len (tail l)))
    0
  )
);
(fun map_of_list l:
  (fun helper idx l:
    (if l
      (let h (head l));
      (let t (tail l));
      (put (helper (+ idx 1) t) idx h)
      {}
    )
  );
  (helper 0 l)
);
(fun distance_to_vowel l:
  (let m (map_of_list l));
  (let max_idx (- (len l) 1));
  (fun search_bwd start idx:
    (if (< idx 0)
      Nil
      (if (is_vowel (get m idx))
        (- start idx)
        (search_bwd start (- idx 1))
      )
    )
  );
  (fun search_fwd start idx:
    (if (> idx max_idx)
      Nil
      (if (is_vowel (get m idx))
        (- idx start)
        (search_fwd start (+ idx 1))
      )
    )
  );
  (fun helper l idx:
    (if l
      (let bwd_dist (search_bwd idx idx));
      (let fwd_dist (search_fwd idx idx));
      (let min_dist (if (== bwd_dist Nil)
        fwd_dist
        (if (== fwd_dist Nil)
          bwd_dist
          (if (< bwd_dist fwd_dist)
            bwd_dist
            fwd_dist
          )
        )
      ));
      (push min_dist (helper (tail l) (+ idx 1)))
      []
    )
  );
  (helper l 0)
);
(distance_to_vowel ["x" "a" "z" "y" "b" "o"])