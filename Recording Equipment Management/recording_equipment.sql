CREATE TABLE public.Brand (
    Brand_ID SERIAL PRIMARY KEY,
    Brand_Name TEXT NOT NULL,
    Country TEXT NOT NULL
);

CREATE TABLE public.Type (
    Type_ID SERIAL PRIMARY KEY,
    Type_Name TEXT NOT NULL
);

CREATE TABLE public.Color (
    Color_ID SERIAL PRIMARY KEY,
    Color_Name TEXT NOT NULL
);

CREATE TABLE public.Supplier (
    Supplier_ID SERIAL PRIMARY KEY,
    Supplier_Name TEXT NOT NULL
);

CREATE TABLE public.Equipment (
    Equipment_ID SERIAL PRIMARY KEY,
    Serial_Number TEXT UNIQUE NOT NULL,
    Condition TEXT NOT NULL,
    Color_ID INT NOT NULL REFERENCES public.Color(Color_ID) ON DELETE CASCADE,
    Brand_ID INT NOT NULL REFERENCES public.Brand(Brand_ID) ON DELETE CASCADE,
    Description TEXT,
    Image_Path TEXT,
    Supplier_ID INT NOT NULL REFERENCES public.Supplier(Supplier_ID) ON DELETE CASCADE,
    Type_ID INT NOT NULL REFERENCES public.Type(Type_ID) ON DELETE CASCADE
);
