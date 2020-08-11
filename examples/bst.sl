(func new_bst_ entry left right:
  (func insert new_entry:
    (if (== entry nil)
      (call new_bst_ new_entry nil nil)
      (let nk (get new_entry "key"));
      (let k (get entry "key"));
      (if (< nk k)
        (if (== left nil)
          (call new_bst_ entry (call new_bst_ new_entry nil nil) right)
          (call new_bst_ entry (call (call left "insert") new_entry) right)
        )
        (if (== right nil)
          (call new_bst_ entry left (call new_bst_ new_entry nil nil))
          (call new_bst_ entry left (call (call right "insert") new_entry))
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
            (call (call left "contains") sk)
          )
          (if (== right nil)
            False
            (call (call right "contains") sk)
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
            (call (call left "search") sk)
          )
          (if (== right nil)
            nil
            (call (call right "search") sk)
          )
        )
      )
    )
  );
  (func print_bst:
    (if (!= left nil)
      (call (call left "print"))
      nil
    );
    (print entry);
    (if (!= right nil)
      (call (call right "print"))
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
  (call new_bst_ nil nil nil)
);
(func entry_bst bst:
  (call bst "entry")
);
(func left_bst bst:
  (call bst "left")
);
(func right_bst bst:
  (call bst "right")
);
(func insert_bst bst new_entry:
  (call (call bst "insert") new_entry)
);
(func contains_bst bst search_key:
  (call (call bst "contains") search_key)
);
(func search_bst bst search_key:
  (call (call bst "search") search_key)
);
(func print_bst bst:
  (call (call bst "print"))
);
(mut bst (call new_bst));
(call print_bst bst);
(print "****");
(set bst (call insert_bst bst {
  "key":3
  "val":"hi"
}));
(call print_bst bst);
(print "****");
(set bst (call insert_bst bst {
  "key":1
  "val":"yo"
}));
(call print_bst bst);
(print "****");
(set bst (call insert_bst bst {
  "key":5
  "val":"sup"
}));
(call print_bst bst);
(print "****");
(set bst (call insert_bst bst {
  "key":5
  "val":"sup"
}));
(call print_bst bst);
(print "****");
(set bst (call insert_bst bst {
  "key":5
  "val":"sup"
}));
(call print_bst bst);
(print "****");
(print (call contains_bst bst 3));
(print (call contains_bst bst 10));
(print (call search_bst bst 1));
(print (call search_bst bst 3));
(print (call search_bst bst 5));
"done!"