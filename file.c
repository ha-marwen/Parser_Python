
prog exemple ;
var x, y : int ;
func fact (n : int) : int ;
{
    if n==0 then {fact=1}
    else
{fact = n*fact(n-1) }
} ;
{
read (x) ;
y =x* x ;
write(fact(x)) ;
write(y)
}