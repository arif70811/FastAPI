from fastapi import *
from schemas import *
from config import *
import psycopg

conn = psycopg.connect(
    f"dbname={DB_Name} user={User} password={Password} host= {Host} port={Port}")

app = FastAPI()

# CRUD Operation for Users

@app.get('/users')
def First_Page():
    Data = conn.execute('select * from public.users order by id').fetchall()
    return Data

@app.get('/users_by_id/{id}')
def get_by_id(id:int):
    Data = conn.execute("""select * from public.users where id = %s""",(id,)).fetchone()
    if not Data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail = f"User of {id} is not Found")
    return Data

@app.post('/create_user')
def Get_posts(user_data:user_creation,status_code=status.HTTP_201_CREATED):
    createdPost = conn.execute(
        "INSERT INTO public.users(email, password)	VALUES ( %s, %s) returning *;",
        (user_data.email,user_data.password)).fetchone() 
    conn.commit()
    if not createdPost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Unable To Create Users")
    return {'Created_Users':createdPost}

@app.put('/update_user/{id}')
def Update_post(id:int,user_data:user_update,status_code=status.HTTP_202_ACCEPTED):
    UpdateData=conn.execute("""UPDATE public.users SET email = %s , password = %s
                            WHERE id = %s returning * """,
                            (user_data.email,user_data.password,id)).fetchall()
    conn.commit()
    if len(UpdateData) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Unable To Update User")
    return {'UpdatedPost':UpdateData}

@app.delete('/delete_user/{id}')
def Delete_User(id:int,status_code = status.HTTP_204_NO_CONTENT):
    Deleted_data=conn.execute("DELETE FROM public.user_post WHERE id = %s returning *",(id,)).fetchall()
    conn.commit()
    if len(Deleted_data)==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User of {id} is not Found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# CRUD Operation for posts

@app.get('/posts')
def get_post():
    Data = conn.execute('select * from public.user_post order by id').fetchall()
    return Data

@app.get('/posts_by_id/{id}')
def get_by_id(id:int):
    Data = conn.execute("""select * from public.user_post where id = %s""",(id,)).fetchone()
    if not Data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail = f"Data of {id} is not Found")
    return Data

@app.post('/create_post')
def Get_posts(post_data:create_post,status_code=status.HTTP_201_CREATED):
    createdPost = conn.execute(
        "INSERT INTO public.user_post(title, content)	VALUES ( %s, %s) returning *;",
        (post_data.Title,post_data.content)).fetchone() 
    conn.commit()
    if not createdPost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Unable To Create Post")
    return {'CreatedPost':createdPost}

@app.delete('/delete_post/{id}')
def delete_by_id(id:int,status_code=status.HTTP_204_NO_CONTENT):
    Deleted_data=conn.execute("DELETE FROM public.user_post WHERE id = %s returning *",(id,)).fetchall()
    conn.commit()
    if len(Deleted_data)==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Data of {id} is not Found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/upate_post/{id}')
def Update_post(id:int,post_data:update_post,status_code=status.HTTP_202_ACCEPTED):
    UpdateData=conn.execute("""UPDATE public.user_post SET title = %s , content = %s , published = %s 
                            WHERE id = %s returning * """,
                            (post_data.Title,post_data.content,post_data.published,id)).fetchall()
    conn.commit()
    if len(UpdateData) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Unable To Update Post")
    return {'UpdatedPost':UpdateData}