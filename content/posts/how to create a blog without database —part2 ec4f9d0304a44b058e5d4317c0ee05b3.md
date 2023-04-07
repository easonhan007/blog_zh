{"title": "how to create a blog without database \u2014part2", "draft": false, "date": "2023-04-07T14:39:24+08:00"}

## Set up the routes

Open the `routes.rb` file and define 3 new rules.

```ruby
Rails.application.routes.draw do
  get 'posts/index'
  get 'posts/show/:file_name', to: 'posts#show', as: 'detail'
  get 'tags/:tag_name', to: 'posts#tag', as: 'tag'
  
  root "posts#index"
end
```

Make the default root path point to the post index page, that is what we expected.

## Create controller

In the terminal, use the rails generator to create a new controller, as  respect to the rails’ convention, I will use posts as the controller’s name instead of post.

```ruby
rails g controller posts index show tag
```

### The post list page

The logic of the post list page is quite straightforward, fetch 100 posts information from post set, to keep it as simple as possible, I did not implement the pagination feature, however since the I selected zset as the primary data structure of post list, it indeed has the potential to paginate all the posts. At the end of the code, I get all the tags from  Redis as well.

```ruby
def index
    key = Rails.configuration.redis['post_set_key']
    tags_key = Rails.configuration.redis['tag_set_key']
    @posts = @r.zrange(key, 0, 100, rev: false)
    Rails.logger.info(@posts)
    @tags = @r.smembers(tags_key)
  end
```

### The post detail page

The post detail page is kind of complicated, the basic idea is trying to get the post detail from redis, if the article’s content does not exist then open the markdown file and render the content directly, at this situation, I will not parse the metadata of the post, in that way the tags will be empty and a line of json string will display at the top of the post page, this is a reasonable feature downgrade.

 

```ruby
def show
    full_file_name = params[:file_name] + ".md"
    file_name = params[:file_name].strip
    file_path = File.join(Rails.root, "posts", full_file_name)
    key_prefix = Rails.configuration.redis['post_prefix']
    key = key_prefix + file_name
    @tags = []
    if @r.exists?(key)
      data = JSON.load @r.get(key)
      @md_content = data['content']
      @tags = data['tags']
      Rails.logger.info("Load from redis")
    else
      if File.exists?(file_path)
        Rails.logger.info("Load from file #{file_path}")
        File.open(file_path) do |f|
          @md_content = f.read
        end
      else
        raise ActionController::RoutingError.new('NOT FOUND')
      end #if 
    end #if
  end
```

### The tags list page

This page is a little bit boring, just get all the tags from redis then render them using the post list page’s template.

```ruby
def tag
    tag = params[:tag_name].strip
    tag_prefix = Rails.configuration.redis['tag_prefix']
    tags_key = Rails.configuration.redis['tag_set_key']

    key = tag_prefix + tag
    @posts = @r.smembers(key)
    @tags = @r.smembers(tags_key)
    render :index
  end
```

## The view

I occasionally found a creative and neat tailwind css blog [template](https://github.com/davidgrzyb/tailwind-blog-template) months ago, I’d like to use the elegant implementation as much as possible. It is a bit long-winded to list the files inside one by one, you can find all the view files I modified a little bit [here](https://github.com/easonhan007/mylog/tree/main/app/views).

## Next step

Our blogging application is now complete, next step I am going  to deploy it to a vm using [capistrano](https://www.notion.so/37c5f2d1d5884fb7a3f82a098fb84a62). It is challenging for to get it all done for beginners, but no worries let’s do it step by step in the next part.