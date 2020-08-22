(func new_bst_ entry left right:
  (func insert new_entry:
    (if (== entry nil)
      (new_bst_ new_entry nil nil)
      (let nk (get new_entry "key"));
      (let k (get entry "key"));
      (if (< nk k)
        (if (== left nil)
          (new_bst_ entry (new_bst_ new_entry nil nil) right)
          (new_bst_ entry ((left "insert") new_entry) right)
        )
        (if (== right nil)
          (new_bst_ entry left (new_bst_ new_entry nil nil))
          (new_bst_ entry left ((right "insert") new_entry))
        )
      )
    )
  );
  (func contains sk:
    (if (== entry nil)
      False
      (let k (get entry "key"));
      (if (== sk k)
        True
        (if (< sk k)
          (if (== left nil)
            False
            ((left "contains") sk)
          )
          (if (== right nil)
            False
            ((right "contains") sk)
          )
        )
      )
    )
  );
  (func search sk:
    (if (== entry nil)
      nil
      (let k (get entry "key"));
      (if (== sk k)
        (get entry "val")
        (if (< sk k)
          (if (== left nil)
            nil
            ((left "search") sk)
          )
          (if (== right nil)
            nil
            ((right "search") sk)
          )
        )
      )
    )
  );
  (func print_bst:
    (if (!= left nil)
      ((left "print"))
      nil
    );
    (print entry);
    (if (!= right nil)
      ((right "print"))
      nil
    )
  );
  (func op o:
    (if (== o "entry")
      entry
      (if (== o "left")
        left
        (if (== o "right")
          right
          (if (== o "insert")
            insert
            (if (== o "contains")
              contains
              (if (== o "search")
                search
                (if (== o "print")
                  print_bst
                  (print "unknown operation")
                )
              )
            )
          )
        )
      )
    )
  )
);
(func new_bst:
  (new_bst_ nil nil nil)
);
(func entry_bst bst:
  (bst "entry")
);
(func left_bst bst:
  (bst "left")
);
(func right_bst bst:
  (bst "right")
);
(func insert_bst bst new_entry:
  ((bst "insert") new_entry)
);
(func contains_bst bst search_key:
  ((bst "contains") search_key)
);
(func search_bst bst search_key:
  ((bst "search") search_key)
);
(func print_bst bst:
  ((bst "print"))
);
(mut bst (new_bst));
(print_bst bst);
(print "****");
(set bst (insert_bst bst {
  "val":"hi"
  "key":3
}));
(print_bst bst);
(print "****");
(set bst (insert_bst bst {
  "val":"yo"
  "key":1
}));
(print_bst bst);
(print "****");
(set bst (insert_bst bst {
  "val":"sup"
  "key":5
}));
(print_bst bst);
(print "****");
(set bst (insert_bst bst {
  "val":"sup"
  "key":5
}));
(print_bst bst);
(print "****");
(set bst (insert_bst bst {
  "val":"sup"
  "key":5
}));
(print_bst bst);
(print "****");
(print (contains_bst bst 3));
(print (contains_bst bst 10));
(print (search_bst bst 1));
(print (search_bst bst 3));
(print (search_bst bst 5));
"done!"