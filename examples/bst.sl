(fun new_bst_ entry left right:
  (fun insert new_entry:
    (if (== entry Nil)
      (new_bst_ new_entry Nil Nil)
      (let nk (get new_entry "key"));
      (let k (get entry "key"));
      (if (< nk k)
        (if (== left Nil)
          (new_bst_ entry (new_bst_ new_entry Nil Nil) right)
          (new_bst_ entry ((left "insert") new_entry) right)
        )
        (if (== right Nil)
          (new_bst_ entry left (new_bst_ new_entry Nil Nil))
          (new_bst_ entry left ((right "insert") new_entry))
        )
      )
    )
  );
  (fun contains sk:
    (if (== entry Nil)
      False
      (let k (get entry "key"));
      (if (== sk k)
        True
        (if (< sk k)
          (if (== left Nil)
            False
            ((left "contains") sk)
          )
          (if (== right Nil)
            False
            ((right "contains") sk)
          )
        )
      )
    )
  );
  (fun search sk:
    (if (== entry Nil)
      Nil
      (let k (get entry "key"));
      (if (== sk k)
        (get entry "val")
        (if (< sk k)
          (if (== left Nil)
            Nil
            ((left "search") sk)
          )
          (if (== right Nil)
            Nil
            ((right "search") sk)
          )
        )
      )
    )
  );
  (fun print_bst:
    (if (!= left Nil)
      ((left "print"))
      Nil
    );
    (print entry);
    (if (!= right Nil)
      ((right "print"))
      Nil
    )
  );
  (fun op o:
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
(fun new_bst:
  (new_bst_ Nil Nil Nil)
);
(fun entry_bst bst:
  (bst "entry")
);
(fun left_bst bst:
  (bst "left")
);
(fun right_bst bst:
  (bst "right")
);
(fun insert_bst bst new_entry:
  ((bst "insert") new_entry)
);
(fun contains_bst bst search_key:
  ((bst "contains") search_key)
);
(fun search_bst bst search_key:
  ((bst "search") search_key)
);
(fun print_bst bst:
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